function setChannel(channel){
    if (channel == '1'){
        data = $('#ch1').serialize()
    }
    if (channel == '2'){
        data = $('#ch2').serialize()
    }
    console.log("Setting channel "+ channel + ' to ' + data);
    $.ajax({
      method: "POST",
      url: "set.json",
      data: data,
      })
}