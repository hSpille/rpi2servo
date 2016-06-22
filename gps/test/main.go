package main

import (
	"fmt"
	"rpipyservo/gps"
)

func main() {

	gps.GpsLocation(func(lat, lon, speed float64) {
		fmt.Println(lat, lon, speed)
	})

}
