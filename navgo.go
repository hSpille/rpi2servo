package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"time"
)

var guiAddr *net.UDPAddr

func reader(r io.Reader) {
	buf := make([]byte, 1024)
	for {
		n, err := r.Read(buf[:])
		if err != nil {
			return
		}
		println("Client got:", string(buf[0:n]))
	}
}

func readFromGui(guiChan chan<- string) {
	ServerAddr, err := net.ResolveUDPAddr("udp", ":10001")
	if err != nil {
		panic(err)
	}
	/* Now listen at selected port */
	ServerConn, err := net.ListenUDP("udp", ServerAddr)
	defer ServerConn.Close()
	buf := make([]byte, 1024)
	for {
		n, addr, err := ServerConn.ReadFromUDP(buf)
		fmt.Println("MSG from GUI: ", string(buf[0:n]), " from ", addr)
		guiAddr = addr
		guiChan <- string(buf[0:n])
		if err != nil {
			fmt.Println("Error: ", err)
		}
	}
}

func readFromGps(gpsChan chan<- string) {
	ServerAddr, err := net.ResolveUDPAddr("udp", ":10002")
	if err != nil {
		panic(err)
	}
	/* Now listen at selected port */
	ServerConn, err := net.ListenUDP("udp", ServerAddr)
	var GuiConnForGpsData net.Conn = nil

	defer ServerConn.Close()
	buf := make([]byte, 1024)
	for {
		n, addr, err := ServerConn.ReadFromUDP(buf)
		fmt.Println("MSG from GPS: ", string(buf[0:n]), " from ", addr)
		gpsChan <- string(buf[0:n])
		if err != nil {
			fmt.Println("Error: ", err)
		}
		if(guiAddr != nil){
			if(GuiConnForGpsData == nil){
				fmt.Println("opening connection to GUI")
				GuiConnForGpsData, err = net.Dial("udp", string(guiAddr.IP.String()) + ":12000")
				if err != nil{
					fmt.Println(err)
				}
			}
			fmt.Println("Sending gps data to client" )
			_, err := GuiConnForGpsData.Write([]byte(string(buf[0:n])))
			if err != nil {
				fmt.Println(err)
			}
		}
	}
}

func main() {
	guiChannel := make(chan string, 1)
	gpsChannel := make(chan string, 1)
	go readFromGui(guiChannel)
	go readFromGps(gpsChannel)

	socketLocation := "/tmp/python_socket.sock"
	//https://golang.org/pkg/net/#Dial
	c, err := net.Dial("unixgram", socketLocation)
	if err != nil {
		panic(err)
	}
	defer c.Close()
	go reader(c)
	for {
		select {
		case msg := <-guiChannel:
			fmt.Println("received message", msg)
			_, err := c.Write([]byte(msg))
			if err != nil {
				panic(err)
			}
			break
		case msg := <-gpsChannel:
			fmt.Println("GPS message", msg)
			break	
		case _ = <-time.NewTicker(1000 * time.Millisecond).C:
			fmt.Println("no message from Gui")
			//Stop the car - we got no news from the controller for too long
			_, err := c.Write([]byte("speed:250"))
			if err != nil {
				log.Fatal("write error:", err)
				break
			}
		}
	}
}
