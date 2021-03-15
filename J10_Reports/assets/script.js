var ui_script = (function(){
  var disableHeaderInput = (function(){
    var inputs = parent.document.getElementsByTagName('table')[1].getElementsByTagName('input');
    for(let i = 0 ; i<inputs.length ; i++){
      inputs[i].disabled = true
    }
  })
  var removeIframeLimit = (async function(){
    await new Promise(r => setTimeout(r, 500));
    parent.document.getElementById('reportPageOutline').style.width = '100%';
    parent.document.getElementById('reportPageOutline').style.height = '100%';
    parent.document.getElementById('reportContent').style.width = null;
    parent.document.getElementById('reportContent').style.height = null;
    parent.document.getElementById('reportPageOutline').style.visibility = 'unset';
  })


  var addToggleButtonListener = (function(){
    parent.document.getElementById('reportPageOutline').style.visibility = 'hidden';
    parent.document.getElementsByClassName('dijitToggleButton')[0].addEventListener("click", async function(){
      await removeIframeLimit();
    });
  })
  return {
    run: function(){
      removeIframeLimit();
      addToggleButtonListener();
      console.log("Remove Iframe Limit")
    },
    disableInput: function(){
      disableHeaderInput();
    }
  }
})();


ui_script.run()
ui_script.disableInput()
