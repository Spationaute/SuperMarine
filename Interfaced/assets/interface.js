let sectionList = [];
let verticalList = [];
let cutsList = [];

function printNewton(id){
    let toRender = "<table>";
    toRender += "<tr><td><label>Mu</label></td><td><input name='mu' type='text' value='0.00089'/></td></tr>";
    toRender += "</table>";
    $(id).html(toRender);
}

function printPowerLaw(id){
    let toRender = "<table>";
    toRender += "<tr><td><label>K</label></td><td><input name='mu' value='0.00089' type='number'/></td></tr>";
    toRender += "<tr><td><label>n</label></td><td><input name='n' value='1' type='number'/></td></tr>";
    toRender += "</table>";
    $(id).html(toRender);
}

function printHB(id) {
    let toRender = "<table>";
    toRender += "<tr><td><label>Gamma Dot </label></td><td><input name='gdot' value='1e-7' type='number'></td></tr>";
    toRender += "<tr><td><label>K</label></td><td><input name='mu' value='0.00089' type='number'></td></tr>";
    toRender += "<tr><td><label>n</label></td><td><input name='n' value='1' type='number'></td></tr>";
    toRender += "</table>";
    $(id).html(toRender);
}

function updateSection(id){
    sectionList[id]= $("#Cadran" + id.toString() + "Size").val();
}
function updateNiveau(id) {
    verticalList[id] = [];
    verticalList[id].push(parseFloat($("#Level" + id.toString() + "Size").val()));
    verticalList[id].push($("#Level" + id.toString() + "Cardan").val());
    verticalList[id].push(parseFloat($("#Level" + id.toString() + "Rotation").val()));
}
function updateCuts(id) {
    cutsList[id] = [];
    cutsList[id].push(parseInt($("#Cuts" + id.toString() + "X").val()));
    cutsList[id].push(parseInt($("#Cuts" + id.toString() + "Y").val()));
    cutsList[id].push(parseInt($("#Cuts" + id.toString() + "Z").val()));
}
function removeSection(id){
    sectionList.splice(id,1);
    renderRadiale("#RadSec");
}
function removeNiveau(id){
    verticalList.splice(id,1);
    renderAxiale("#VertSec");
}
function removeCuts(id){
    cutsList.splice(id,1);
    renderCuts("#CutsSec");
}
function renderCuts(div) {
    let list = cutsList;
    let toRender ="<table>";
    toRender += "<tr><td><b>#</b></td><td><b>Cadran (r)</b></td><td><b>Secteur (theta)</b></td><td><b>Niveau (z)</b></td><td></td></tr>";
    let nlist = list.length;
    for(let ii=0;ii<nlist;++ii){
        toRender += "<tr>";
        toRender += "<td>"+ii.toString()+"</td>";
        toRender += "<td><input id='Cuts"+ii.toString()+"X' type='number' min='0' step='1' value='"+list[ii][0].toString()+"' oninput='updateCuts("+ii.toString()+")'/></td>";
        toRender += "<td><input id='Cuts"+ii.toString()+"Y' type='number' min='0' step='1' value='"+list[ii][1].toString()+"' oninput='updateCuts("+ii.toString()+")'/></td>";
        toRender += "<td><input id='Cuts"+ii.toString()+"Z' type='number' min='0' step='1' value='"+list[ii][2].toString()+"' oninput='updateCuts("+ii.toString()+")'/></td>";
        toRender += "<td><input type=\"button\" value=\"-\" style='width:100%' onclick='removeCuts("+ii.toString()+")'></td>";
        toRender += "</tr>";
    }
    toRender += "<tr><td colspan='5'><input id=\"cutsAdd\" type=\"button\" style='width:100%' value=\"+\"></td></tr></table>";
    toRender += "</table>";
    $(div).html(toRender);

    $('#cutsAdd').click(()=>{
        cutsList.push([0,0,0]);
        renderCuts("#CutsSec");
    });
}
function renderRadiale(div){
    let list = sectionList;
    let toRender ="<table>";
    toRender += "<tr><td><b>Niveau</b></td><td><b>Taille</b></td><td></td></tr>";
    toRender += "<tr>";
        toRender += "<td>Centre</td>";
        toRender += "<td><input id=\"radCentre\" type=\"number\" value='0.010' step='0.001'/></td>";
        toRender += "<td></td>";
    toRender += "</tr>";
    let nlist = list.length;
    for(let ii=0;ii<nlist;++ii){
        toRender += "<tr>";
            toRender += "<td>Cadran "+ii.toString()+"</td>";
            toRender += "<td><input id='Cadran"+ii.toString()+"Size' type=\"number\" step='0.001' value='"+list[ii].toString()+"' oninput='updateSection("+ii.toString()+")'/></td>";
            toRender += "<td><input type=\"button\" value=\"-\" style='width:100%' onclick='removeSection("+ii.toString()+")'>";
        toRender += "</tr>";
    }
    toRender += "<tr><td colspan='3'><input id=\"radialAdd\" type=\"button\" value=\"+\" style='width:100%'></td></tr></table>";
    $(div).html(toRender);

    $('#radialAdd').click(()=>{
        if(sectionList.length>0) {
            let lastRadii = sectionList[sectionList.length - 1];
            sectionList.push(lastRadii + 0.01);
        }else {
            sectionList.push(0.020);
        }
        renderRadiale("#RadSec");
    });
}

function renderAxiale(div){
    let list=verticalList;
    let toRender ="<table>";
    toRender += "<tr><td><b>Niveau</b></td><td><b>Taille</b></td><td><b>Cardan</b></td><td><b>Rotation</b></td><td></td></tr>";
    toRender += "<tr>";
        toRender += "<td>Niveau 0</td>";
        toRender += "<td><input id='botN' value='0.01' type=\"number\"/></td>";
        toRender += "<td><input id='botImp' type='checkbox'/></td>";
        toRender += "<td><input id='botRot' value='0.00' type='number'/></td>";
        toRender += "<td></td>";
    toRender += "</tr>";
    let nlist = list.length;
    for(let ii=0;ii<nlist;++ii){
        toRender += "<tr>";
            toRender += "<td>Niveau "+(ii+1).toString()+"</td>";
            toRender += "<td><input  id='Level"+ii.toString()+"Size' value='"+list[ii][0].toString()+"' type=\"number\" oninput='updateNiveau("+ii.toString()+")'/></td>";
            toRender += "<td><input  id='Level"+ii.toString()+"Cardan' value='"+list[ii][1].toString()+"' type='checkbox' oninput='updateNiveau("+ii.toString()+")'/></td>";
            toRender += "<td><input  id='Level"+ii.toString()+"Rotation' value='"+list[ii][2].toString()+"' type='number' oninput='updateNiveau("+ii.toString()+")'/></td>";
            toRender += "<td><input type=\"button\" style='width:100%' value=\"-\" onclick='removeNiveau("+ii.toString()+")'>";
        toRender += "</tr>";
    }
    toRender += "<tr><td colspan='5'><input id=\"vertAdd\" type=\"button\" style='width:100%' value=\"+\"></td></tr></table>";
    $(div).html(toRender);

    $('#vertAdd').click(()=>{
       verticalList.push([0.02,"off",0]);
       renderAxiale("#VertSec");
    });
}
function buildBMData() {
    let data = {
        "centre":parseFloat($("#radCentre").val()),
        "sections":sectionList,
        "bottom":[
            parseInt($("#botN").val()),
            parseInt($("#botImp").val()),
            parseInt($("#botRot").val())],
        "vertical":verticalList,
        "cuts":cutsList,
        "nsec":parseInt($("#sectionSlider").val()),
        "coeur":parseFloat($("#coeurSlider").val()),
        "division":[
            parseInt($("#divR").val()),
            parseInt($("#divTheta").val()),
            parseInt($("#divZ").val())]
    };
    return data;
}

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

function sendMeshBM() {
    let toSend = buildBMData();
    toSend["type"]="blockMesh";
    $.ajax("/gen",{
        data:JSON.stringify(toSend),
        contentType:"application/json",
        method:"POST",
        dataType:"text",
        success:function (inData,status,jq) {
            console.log("Receiving....");
            let data = JSON.parse(inData);
            if(data["status"]==="ready") {
                download("blockMeshDict", data["data"]);
            }else{
                console.log("Querry Error 1001");
            }
        }
    });
}

function sendMeshPY() {
    let toSend = buildBMData();
    toSend["type"]="python";
    $.ajax("/gen",{
        data:JSON.stringify(toSend),
        contentType:"application/json",
        method:"POST",
        dataType:"text",
        success:function (inData,status,jq) {
            console.log("Receiving....");
            let data = JSON.parse(inData);
            if(data["status"]==="ready") {
                download("superMarine.py", data["data"]);
            }else{
                console.log("Querry Error 1001");
            }
        }
    });
}

function main(){
    $("#sectionNum").html("4");
    $("#coeurProp").html("0.62");

    renderRadiale("#RadSec");
    renderAxiale("#VertSec");
    renderCuts("#CutsSec");
    printNewton('#fluidOne');
    printNewton('#fluidTwo');

    $("#sendButtonBM").click(()=>{
        sendMeshBM();
    });

    $("#sendButtonPY").click(()=>{
        sendMeshPY();
    });

    $("#sectionSlider").change(()=>{
        let N=$("#sectionSlider").val();
        $('#sectionNum').html(N.toString());
    });

    $("#coeurSlider").change(()=>{
        let N=$("#coeurSlider").val();
        $('#coeurProp').html(N.toString());
    });

    $("#selectF1").change(()=>{
        let model = $("#selectF1").val();
        if(model === "Newton"){
            printNewton("#fluidOne");
        }else if(model === "PowerLaw"){
            printPowerLaw("#fluidOne");
        }else if(model === "HB"){
            printHB('#fluidOne');
        }
    });

    $("#selectF2").change(()=>{
        let model = $("#selectF2").val();
        if(model === "Newton"){
            printNewton("#fluidTwo");
        }else if(model === "PowerLaw"){
            printPowerLaw("#fluidTwo");
        }else if(model === "HB"){
            printHB('#fluidTwo');
        }
    });
}

$(main);
