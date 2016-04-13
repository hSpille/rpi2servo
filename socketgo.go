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

func main() {
	ServerAddr, err := net.ResolveUDPAddr("udp", ":10001")

	/* Now listen at selected port */
	ServerConn, err := net.ListenUDP("udp", ServerAddr)
	defer ServerConn.Close()

	buf := make([]byte, 1024)

	for {
		n, addr, err := ServerConn.ReadFromUDP(buf)
		fmt.Println("Received ", string(buf[0:n]), " from ", addr)

		if err != nil {
			fmt.Println("Error: ", err)
		}
	}

	socketLocation := "/tmp/python_socket.sock"

	//https://golang.org/pkg/net/#Dial
	c, err := net.Dial("unixgram", socketLocation)
	if err != nil {
		panic(err)
	}
	defer c.Close()

	go reader(c)
	for {
		_, err := c.Write([]byte("hi"))
		if err != nil {
			log.Fatal("write error:", err)
			break
		}
		time.Sleep(1e9)
	}
}
