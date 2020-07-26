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
      })
}