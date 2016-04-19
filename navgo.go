package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"time"
)

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
		guiChan <- string(buf[0:n])
		if err != nil {
			fmt.Println("Error: ", err)
		}
	}
}

func main() {
	guiChannel := make(chan string, 1)
	go readFromGui(guiChannel)
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
		case _ = <-time.NewTicker(1000 * time.Millisecond).C:
			fmt.Println("no message from Gui")
			_, err := c.Write([]byte("nop"))
			if err != nil {
				log.Fatal("write error:", err)
				break
			}
		}
	}
}
