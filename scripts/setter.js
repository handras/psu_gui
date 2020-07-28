function setChannel(channel, turn_on){
    if (channel == '1'){
        data = $('#ch1').serialize()
        data += "&ch1_state="+turn_on
    }
    if (channel == '2'){
        data = $('#ch2').serialize()
        data += "&ch2_state="+turn_on
    }
    console.log("Setting channel "+ channel + ' to ' + turn_on + " with " + data);
    $.ajax({
      method: "POST",
      url: "set.json",
      data: data,
      success: (data)=>{
        console.log("PSU set successfully");
        $("#success-alert").html("Values set successfully!");
        $("#success-alert").show(150).delay(1550).hide(120);
      },
      timeout: 1800,
      error: (jqXHR, status, error)=>{
        console.log("Error occurred: " + status);
        $("#failure-alert").html("Error occurred during setting the values: " + status);
        $("#failure-alert").show(150).delay(1850).hide(120);
      }
    })
}

function setChannelOff(channel){
    console.log("SettingOff channel "+ channel);
    $.ajax({
      method: "POST",
      url: "setOff.json",
      data:{"ch":channel},
      success:()=>{console.log("Sent turnoff data!")}
      })
}