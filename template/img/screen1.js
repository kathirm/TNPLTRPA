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

var selectedop = [];
var userAmount=0,usrsubAmount=0;
var pDetails={};
function totalIt(event) {
    
    if(localStorage.getItem('paymentCalc')){
       // pDetails=JSON.parse(localStorage.getItem("paymentCalc"));
        localStorage.setItem("paymentCalc",false);
    }

    
    var currentuser = document.getElementById("usercnt").value;

    var exuser = (currentuser == "" ) ? 0 : currentuser ;
    var totAmt= '';
    var fulamt= '';
    var op1= document.getElementById("orderProduct")
        op1.innerHTML = "";
    var ary = [];
    var productAmt={crm:50,wms:50,hr:50};
    if(event.target.selectedOptions){
        selectedop = event.target.selectedOptions
    }else{
        selectedop =pDetails.selectedPack;
        }

    for(var i=0;i<selectedop.length;i++){
        var pAmount;
        akey= Object.keys(productAmt)

            for(var j=0;j<akey.length;j++){
                if(selectedop[i].value == akey[j]){
                    pAmount = productAmt[akey[j]];
                }else{
                    if(selectedop[i]==akey[j]){
                    pAmount = productAmt[akey[j]];
                    }
                }
            }
            var labelName= selectedop[i].label?selectedop[i].label:selectedop[i].toUpperCase();
        var data =' <div class="col-sm-6"> '+labelName+'</div><div class="col-sm-1 text-right">1</div> <div class="col-sm-5 text-right"><input type="text" style="width: 72%;text-align: center;" required readonly="readonly" value="'+pAmount+'" id="box1"></div>'

            op1.innerHTML=op1.innerHTML + data;
        totAmt = Number(totAmt) + Number(pAmount);
        user_count_val = Number(exuser)>0? Number(exuser) - 1 :0;
        userAmount = user_count_val * 10 ;
        usrsubAmount = userAmount + totAmt ;
        ary.push(selectedop[i].value?selectedop[i].value:selectedop[i]);
    }
    pDetails.selectedPack=ary;
    obj['productType']=ary;
    document.getElementById("box2").value=totAmt;
    document.getElementById("packusers").innerHTML = exuser.toString();
    document.getElementById("box3").value = userAmount
    document.getElementById("totalresult").value=usrsubAmount;
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
