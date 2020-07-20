
//Globals
var refresh_rate_value = 1500;

function update_usage(data){
    $.each(data, function( key, val ) {
        document.getElementById(key).innerText = val;
    });
}

function refresh(){
    jQuery.ajax({
      method: "GET",
      dataType: "json",
      url: "current.json",
      success:update_usage
    })
    if (refresh_rate_value > 0.1)
        setTimeout(refresh,refresh_rate_value);
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
refresh();
