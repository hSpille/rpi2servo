package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net"
	"rpi2servo/gps"
	"time"
)

var guiAddr *net.UDPAddr

type GpsMessage struct {
	Lat   float64
	Long  float64
	Speed float64
}

type GyroMessage struct {
	ax float64
	ay float64
	az float64
	gx float64
	gy float64
	gz float64
}

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

func readFromGyro(gyroChan chan<- string) {
	gSocket, err := net.Dial("unix", "/tmp/gyro_socket.sock")
	if err != nil {
		panic(err)
	}
	defer gSocket.Close()
	_, err = gSocket.Write([]byte("hello"))
	if err != nil {
		panic(err)
	}
	buf := make([]byte, 1024)
	for {
        n, err := gSocket.Read(buf[:])
        if err != nil {
            panic(err)
        }
        data := buf[0:n]
		gyroChan <- string(data)
	}
}

func readFromGps(gpsChan chan<- string) {
	var GuiConnForGpsData net.Conn = nil
	gps.GpsLocation(func(lat, lon, speed float64) {
		gpsLocation := GpsMessage{lat, lon, speed}
		jsonGps, err := json.Marshal(&gpsLocation)
		if err != nil {
			fmt.Println("Error", err)
		}
		gpsChan <- string(jsonGps)
		if guiAddr != nil {
			if GuiConnForGpsData == nil {
				GuiConnForGpsData, _ = net.Dial("udp", string(guiAddr.IP.String())+":12000")
			}
			_, err := GuiConnForGpsData.Write(jsonGps)
			if err != nil {
				fmt.Println(err)
			}
		}
	})
}

func main() {
	guiChannel := make(chan string, 1)
	gpsChannel := make(chan string, 1)
	gyroChannel := make(chan string, 1)
	go readFromGui(guiChannel)
	go readFromGps(gpsChannel)
	go readFromGyro(gyroChannel)

	socketLocation := "/tmp/python_socket.sock"
	//https://golang.org/pkg/net/#Dial
	c, err := net.Dial("unixgram", socketLocation)
	if err != nil {
		fmt.Println("Gui sock problem!")
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
				fmt.Println("Gui recv problem!")
				panic(err)
			}
			break
		case msg := <-gpsChannel:
			fmt.Println("GPS message", msg)
			break
		case msg := <- gyroChannel:
			fmt.Println("Gyro message", msg)
			break
		case _ = <-time.NewTicker(1000 * time.Millisecond).C:
			fmt.Println("no message from Gui")
			//Stop the car - we got no news from the controller for too long
			_, err := c.Write([]byte("speed:250"))
			if err != nil {
				fmt.Println("Fatal write error")
				log.Fatal("write error:", err)
				break
			}
		}
	}
}
