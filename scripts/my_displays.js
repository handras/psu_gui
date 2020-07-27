var ch1_v_display = new SegmentDisplay("ch1_v");
var ch1_i_display = new SegmentDisplay("ch1_i");
var ch2_v_display = new SegmentDisplay("ch2_v");
var ch2_i_display = new SegmentDisplay("ch2_i");

var displays = [ch1_v_display, ch1_i_display, ch2_v_display, ch2_i_display];
displays.forEach((d)=>{
    d.pattern         = "##.##";
    d.displayAngle    = 8;
    d.digitHeight     = 20;
    d.digitWidth      = 10;
    d.digitDistance   = 2.5;
    d.segmentWidth    = 2.1;
    d.segmentDistance = 0.8;
    d.segmentCount    = 7;
    d.cornerType      = 1;
    d.colorOn         = "#ff2c14";
    d.colorOff        = "#3a161b";
    d.draw();
})
