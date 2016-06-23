package gps

// #cgo LDFLAGS: -lgps -lm
// #include <gps.h>
import "C"
import "fmt"

type GpsLocationCallback func(float64, float64, float64)

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
			cb(lat, lon, speed)
		} else {
			fmt.Println("No GPS fix:", data.fix.mode)
		}
	}
}
