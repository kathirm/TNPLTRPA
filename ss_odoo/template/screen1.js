function isNumber(evt){
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    return true; }


function confirmEmail() {
    var email = document.getElementById("mailvalidate").value
    var confemail = document.getElementById("confirmmailvalidate").value
    if(email != confemail) {
        alert('Email Not Matching!');
    }
}


function totalIt(event) {
    var totAmt= '';
    var op1= document.getElementById("orderProduct")
    op1.innerHTML = "";
    var ary = [];
    var productAmt=[10,20,30];
    // var variableName=event.target.name;
    for(var i=0;i<event.target.selectedOptions.length;i++){
    var data =' <div class="col-sm-6"> '+event.target.selectedOptions[i].label+'</div><div class="col-sm-1 text-right">1</div> <div class="col-sm-5 text-right"><input type="text" style="width: 72%;text-align: center;" readonly="readonly" value="'+productAmt[i]+'" id="box1"></div>'
    op1.innerHTML=op1.innerHTML + data;
    totAmt = Number(totAmt) + Number(productAmt[i]);
    ary.push(event.target.selectedOptions[i].label);
    }
    obj['productType']=ary;
    obj["totalAmount"]=totAmt;
    document.getElementById("totalresult").value=totAmt;
    document.getElementById("box2").value=totAmt;
    }

  function submitform(event){

    //   var crdt= document.getElementById("credit").value;
    //  var cardno= document.getElementById("cardnumber").value;
    //  var nameofholder= document.getElementById("nameofcardholder").value;
    //  var code= document.getElementById("securitycode").value;
    //  var ins= document.getElementById("install").value;
    //  var zipcodee= document.getElementById("zipcode").value;
    //  var fullname= document.getElementById("fullname").value;
    //  var cnpj= document.getElementById("cnpj").value;
    //  var mail= document.getElementById("mailvalidate").value;
    //  var cnfrmmail= document.getElementById("confirmmailvalidate").value;
    //  var totalres= document.getElementById("totalresult").value;

    //  alert(cardno);
  }
var obj = {};
  function cardselection(event){
   var variableName=event.target.name;
   //varialeName= event.target.value;
   if(variableName!="install"){
   obj[variableName]=event.target.value;  
       
   }
   else{
    var ary = [];
    for(var i=0;i<event.target.selectedOptions.length;i++){
        ary.push(event.target.selectedOptions[i].label.toLowerCase());
    }
    obj['productType']=ary;
   }
   console.log(obj);

  }