var module = (function(){
    /*
        The default value of the filters for particular report
        Change accordingly based on report filter / default value
    */
    var defaultValue = [
        "PP","Semua","Semua","Semua","Semua","Semua","Semua","table/html;page-mode=page"
    ];
    var selects = (function(){
        //parent or not parent
        return parent.document.getElementsByTagName("select")
    })
    var getDefaultSelects = (function(param){
        for(let i = 0 ; i < param.length ; i++){
            defaultValue.push(param[i].value)
        }
    })

    var bindExistResetButton = (function(){
        let button = parent.document.getElementById("resetButton")
        button.onclick = reset
    })

    var checkResetButtonExist = (function(){
        let button = parent.document.getElementById("resetButton")
        return button != null ? true : false
    })
    var reset = (function(){
        let param = selects()
        for(let i = 0 ; i < param.length; i++){
            param[i].value = defaultValue[i]
            param[i].dispatchEvent(new Event('change'));
        }
    })
    var appendResetButton = (function(param,button){
        param[param.length-1].insertAdjacentElement("afterend",button)
    })
    var resetButton = (function(){
        let button = document.createElement("button")
        button.id = "resetButton"
        button.innerHTML = "Reset"
        button.onclick = reset
        button.className = "pentaho-button"
        button.style.marginLeft = "10px"
        button.style.background = "gray"
        return button
    })

    return {
        init: function(){
            console.log(checkResetButtonExist())
            if(!checkResetButtonExist()){
                let param = selects()
                //getDefaultSelects(param)
                let rb = resetButton()
                appendResetButton(param,rb)
            } else {
                bindExistResetButton()
            }
        }
    }
}());

module.init()