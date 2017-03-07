package main

//Test a socket with socat like: socat - UNIX-CONNECT:/tmp/gps_socket

// #cgo LDFLAGS: -lgps -lm
// #include <gps.h>
import "C"
import "fmt"
import "net"
import "encoding/json"
import "os"
import "sync"

type GpsMessage struct {
	Lat   float64
	Long  float64
	Speed float64
}

type GpsLocationCallback func(float64, float64, float64) bool

func GpsLocation(cb GpsLocationCallback) {
	var data C.struct_gps_data_t
	C.gps_open(C.CString("localhost"), C.CString("2947"), &data)
	C.gps_stream(&data, 0x000001|0x000010, nil)
	for {
		C.gps_waiting(&data, 2000000)
		C.gps_read(&data)
		if data.fix.mode == 2 || data.fix.mode == 3 {
			lat := float64(data.fix.latitude)
			lon := float64(data.fix.longitude)
			speed := float64(data.fix.speed)
			if cb(lat, lon, speed) {
				break
			}
		} else {
			fmt.Println("No GPS fix:", data.fix.mode)
		}
	}
}

func readGps(conn *net.UnixConn) {
	defer conn.Close()
	GpsLocation(func(lat, lon, speed float64) bool {
		gpsLocation := GpsMessage{lat, lon, speed}
		jsonGps, err := json.Marshal(&gpsLocation)
		if err != nil {
			fmt.Println("Error", err)
		}
		_, err = conn.Write([]byte(jsonGps))
		if err != nil {
			fmt.Println("Client disconnect:", err)
			return true
		}
		return false
	})
}

func main() {
	l, err := net.ListenUnix("unix", &net.UnixAddr{"/tmp/gps_socket", "unix"})
	if err != nil {
		panic(err)
	}

	var connections []*net.UnixConn
	var connectionsMu sync.Mutex

	go func() {
		defer os.Remove("/tmp/gps_socket")
		for {
			conn, err := l.AcceptUnix()
			if err != nil {
				panic(err)
			}

			connectionsMu.Lock()
			connections = append(connections, conn)
			connectionsMu.Unlock()

			// b := []byte("hi")
			// _, err = conn.Write(b)
			// readGps(conn)
			//       if err != nil {
			//           panic(err)
			//       }
		}
	}()

	GpsLocation(func(lat, lon, speed float64) bool {
		gpsLocation := GpsMessage{lat, lon, speed}
		jsonGps, err := json.Marshal(&gpsLocation)
		if err != nil {
			fmt.Println("Error", err)
		}
		var toRemove []int
		connectionsMu.Lock()
		var index int = 0
		for _, conn := range connections {
			index++
			_, err = conn.Write([]byte(jsonGps))
			if err != nil {
				fmt.Println("Client disconnect:", err)
				toRemove = append(toRemove, index)
			}
		}
		if len(toRemove) > 0 {
			for i := 0; i < index; i++ {
				connections = append(connections[:i], connections[i+1:]...)
			}
		}
		connectionsMu.Unlock()
		return false
	})

}
