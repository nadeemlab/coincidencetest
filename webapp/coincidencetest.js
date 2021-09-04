function setup(){
  document.getElementById('uploadbutton').addEventListener('change', openDialog);

  var obj_csv = {
      size:0,
      dataFile:[]
  };

  function openDialog() {
    // const input = document.querySelector('input[type="file"]');
    // const file = input.files[0];
    // input = document.getElementById('uploadbutton')
    document.getElementById('progressarea').hidden = false
    input = document.getElementById('uploadbutton')
    readImage(input)

    setTimeout(function(){
      document.getElementById('progressarea').hidden = true
    }, 2000);
    
  }
   
  function readImage(input) {
      console.log(input)
      console.log('...')
   if (input.files && input.files[0]) {
   let reader = new FileReader();
          reader.readAsBinaryString(input.files[0]);
   reader.onload = function (e) {
   console.log(e);
   obj_csv.size = e.total;
   obj_csv.dataFile = e.target.result
              console.log(obj_csv.dataFile)
              parseData(obj_csv.dataFile)
              document.getElementById('area').innerHTML = obj_csv.dataFile

   }
   }
  }
   
  function parseData(data){
      let csvData = [];
      let lbreak = data.split("\n");
      lbreak.forEach(res => {
          csvData.push(res.split("\t"));
      });
      console.table(csvData);
  }

}
