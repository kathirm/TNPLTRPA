function isNumber(evt){
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
    return false;
    }
    return true; 
}

var count = "";
var packamnt = 50;
var usrten = 10;
var selectedPack=[];

function prd(event){
    var gtuser = document.getElementById("usercnt").value;
    document.getElementById("peruser").innerHTML = gtuser;
    var usersCount =Number(gtuser)>0? Number(gtuser) - 1 :0;
     var userpackcost = (usersCount * usrten)
        document.getElementById("useramount").innerText = userpackcost;
    if(event.target.checked){

        count= Number(count) + 1 
        selectedPack.push(event.target.value)
       
    }
    else{
        if(event.target.type == "checkbox"){
            count = count - 1;
            var pos =selectedPack.indexOf(event.target.value)
            selectedPack.splice(pos,1);
          }
    } 
         var modules = count*packamnt;
         document.getElementById("permodule").innerText =count;
         document.getElementById("modulecount").innerHTML = modules;
         var demototal = (userpackcost) + (modules) ;
         document.getElementById("totalamount").innerText = count && demototal.toString()||0;
        if(gtuser>0 && Number(count)!=0){
         localStorage.setItem("paymentCalc",JSON.stringify({
            userCount:gtuser,selectedPack:selectedPack,
            userCost:userpackcost,modulesCount: count,modulesCost:modules,totalAmount:demototal}));
         }else{
             localStorage.setItem("paymentCalc",false)
         }

         }



function checkoutEventChange(event){
    var gtuser = document.getElementById("usercnt").value;
    if(gtuser&&Number(count)!=0){
        var frm = document.getElementsByName('contact-form')[0];
        frm.submit();
        frm.reset();
    }else{
        console.log(Number(count))
        event.preventDefault();
        alert("please file the content.\n user or pack is not filled");
        
    }

}         