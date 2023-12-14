let l_r = 0,
    l_g = 255,
    l_b = 0,

    d_r = 0,
    d_g = 255,
    d_b = 0;

let tolerance = 0.05;

let processor = {
  timerCallback: function() {
    if (this.video.paused || this.video.ended) {
      return;
    }
    this.computeFrame();
    let self = this;
    setTimeout(function () {
        self.timerCallback();
      }, 0);
  },

  doLoad: function() {
    this.video = document.getElementById("video");
    this.c1 = document.getElementById("c1");
    this.ctx1 = this.c1.getContext("2d");
    this.c2 = document.getElementById("c2");
    this.ctx2 = this.c2.getContext("2d");
    let self = this;
    this.video.addEventListener("play", function() {
        self.width = self.video.videoWidth;
        self.height = self.video.videoHeight;
        self.timerCallback();
      }, false);
  },

  calculateDistance: function(c, min, max) {
      if(c < min) return min - c;
      if(c > max) return c - max;

      return 0;
  },

  computeFrame: function() {
    this.ctx1.drawImage(this.video, 0, 0, this.width, this.height);
    let frame = this.ctx1.getImageData(0, 0, this.width, this.height);
        let l = frame.data.length / 4;

    for (let i = 0; i < l; i++) {
      let _r = frame.data[i * 4 + 0];
      let _g = frame.data[i * 4 + 1];
      let _b = frame.data[i * 4 + 2];

      let difference = this.calculateDistance(_r, d_r, l_r) + 
                       this.calculateDistance(_g, d_g, l_g) +
                       this.calculateDistance(_b, d_b, l_b);
      difference /= (255 * 3); // convert to percent
      if (difference < tolerance)
        frame.data[i * 4 + 3] = 0;
    }
    this.ctx2.putImageData(frame, 0, 0);
    return;
  }
};