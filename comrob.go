// package main is the main package of the comrob project
package main

import (
	"fmt"
	"net"
)

func main() {
	address := "localhost:10002"
	_, err := net.Dial("tcp", address)
	if err != nil {
		fmt.Println(err)
		return
	}
}