function isNumber(evt){
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
    return false;
    }
    return true; 
}

function Monthlyprice(event){

var multi = document.getElementById("multifive").value;
document.getElementById("peruser").innerHTML =multi;
packamnt = (multi/5)*50;
document.getElementById("useramount").innerHTML =packamnt;

if(event.target.value == 0){
 document.getElementById("totalamount").innerText ="";
}else{
  document.getElementById("totalamount").innerText =(packamnt *count).toString();
}
}

function usertotal(event){
 var userAmount = document.getElementById("peruser").value;
 document.getElementById("useramount").innerHTML = userAmount;
}



var count = "";
function prd(event){
if(event.target.checked){
  count= Number(count) + Number(event.target.value);
}
else{
  count= Number(count) - 1;
}
 document.getElementById("permodule").innerText =count.toString();
 document.getElementById("modulecount").innerText =count.toString();
 document.getElementById("totalamount").innerText =(packamnt *count).toString();

}
