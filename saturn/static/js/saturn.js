function switchforms(){
    if (document.getElementById("prescriberradio").checked) {
      document.getElementById("prescriberform").style.display = "block";
      document.getElementById("drugform").style.display = "none";
  }
  else if (document.getElementById("drugradio").checked) {
    document.getElementById("prescriberform").style.display = "none";
    document.getElementById("drugform").style.display = "block";
  }
}

function switchedit(){
  if (document.getElementById("prescriberradio").checked) {
    document.getElementById("prescriberform").style.display = "block";
    document.getElementById("drugform").style.display = "none";
}
else if (document.getElementById("drugradio").checked) {
  document.getElementById("prescriberform").style.display = "none";
  document.getElementById("drugform").style.display = "block";
}

}

function yeet(){
  fname = document.getElementById("firstname").value;
  lname = document.getElementById("lastname").value;
  alert("Sucessfully Created Presriber: " + fname + ' ' + lname);
}

// Script to open and close sidebar
function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("myOverlay").style.display = "block";
  }
   
  function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
    document.getElementById("myOverlay").style.display = "none";
  }
  
  // Modal Image Gallery
  function onClick(element) {
    document.getElementById("img01").src = element.src;
    document.getElementById("modal01").style.display = "block";
    var captionText = document.getElementById("caption");
    captionText.innerHTML = element.alt;
  }

  function switchedit() {
    if (document.getElementById("radioedit").checked) {
      document.getElementById("presriberedit").style.display = "none";
      document.getElementById("prescriberform").style.display = "block";
      document.getElementById("tripleform").style.display = "none";
  }
  
  else {
    document.getElementById("prescriberform").style.display = "none";
    document.getElementById("presriberedit").style.display = "block";
    document.getElementById("tripleform").style.display = "none";
  }
  }
  
  function tripleedit(){
     if (document.getElementById('triple').checked){
      document.getElementById("presriberedit").style.display = "none";
      document.getElementById("prescriberform").style.display = "none";
      document.getElementById('tripleform').style.display = 'block';
    
    }
    else{
      document.getElementById("prescriberform").style.display = "none";
      document.getElementById('tripleform').style.display = 'none';
      document.getElementById("presriberedit").style.display = "block";
    }
  }

  // function letsgo(){
  //   x = document.getElementById('drug')
  //   document.getElementById('qty').min = str(document.getElementById(x) * -1)

  // }