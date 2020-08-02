
//Globals
var refresh_rate_value = 1500;

function update_usage(data){
//    console.log("new data",data)
    ping = new Date - ping;
    $('#network_latency').html("Network latency (ms): " + ping);
    ch1_v_display.setValue(data["ch1_volt_usage"]);
    ch1_i_display.setValue(data["ch1_amp_usage"]);
    $("#ch1_state").bootstrapToggle('enable')
    if (data["ch1_state"] == 1){
        $("#ch1_state").bootstrapToggle('on')
    }
    else{
        $("#ch1_state").bootstrapToggle('off')
    }
    $("#ch1_state").bootstrapToggle('disable')

    ch2_v_display.setValue(data["ch2_volt_usage"]);
    ch2_i_display.setValue(data["ch2_amp_usage"]);
    $("#ch2_state").bootstrapToggle('enable')
    if (data["ch2_state"] == 1){
        $("#ch2_state").bootstrapToggle('on')
    }
    else{
        $("#ch2_state").bootstrapToggle('off')
    }
    $("#ch2_state").bootstrapToggle('disable')
}

function refresh(){
    ping = new Date;
    jQuery.ajax({
      method: "GET",
      dataType: "json",
      url: "current.json",
      success:update_usage,
      timeout: 3200,
      error: (jqXHR, status, error)=>{
        console.log("Error occurred: " + status);
        $("#failure-alert").html("Error occurred during reading usage values: " + status);
        $("#failure-alert").show(150).delay(2050).hide(120);
      },
      complete:()=>{
        if (refresh_rate_value > 0.1)
            setTimeout(refresh,refresh_rate_value);
      }
    })

}

// Instantiate a slider
var refreshSlider = new Slider("#refresh_rate", {
	min:0,
	max:5,
	value:0,
	step:0.5,
	formatter: function(value) {
	    if(value < 0.5)
	        return "Off";
		return ''+value;
	}
});
refresh_rate_value = refreshSlider.getValue()
refreshSlider.on('slideStop', function(new_value){
    let old_rate = refresh_rate_value
    refresh_rate_value = new_value * 1000;
    console.log("Refresh rate is set to: " + refresh_rate_value)
    if (old_rate < 0.1)
        refresh()
})

console.log("refresher script start");
ping = new Date;
refresh();
