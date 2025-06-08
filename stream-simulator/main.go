package main

import (
	"fmt"
	"log"
	"net/http"
	"time"

	"gocv.io/x/gocv"
)

func main() {
	video, err := gocv.VideoCaptureFile("movies/video.mp4")
	if err != nil {
		fmt.Println("Error on open movie:", err)
	}
	defer video.Close()

	img := gocv.NewMat()
	defer img.Close()

	http.HandleFunc("/stream", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "multipart/x-mixed-replace; boundary=frame")

		for {
			if ok := video.Read(&img); !ok || img.Empty() {
				video.Set(gocv.VideoCapturePosFrames, 0)
				continue
			}

			buf, _ := gocv.IMEncode(".jpg", img)

			fmt.Fprintf(w, "--frame\r\nContent-Type: image/jpeg\r\n\r\n")
			w.Write(buf.GetBytes())
			fmt.Fprintf(w, "\r\n")

			if f, ok := w.(http.Flusher); ok {
				f.Flush()
			}
			time.Sleep(33 * time.Millisecond) // ~30 FPS
		}
	})

	fmt.Println("Server online in http://localhost:8081/stream")
	log.Fatal(http.ListenAndServe(":8081", nil))
}
