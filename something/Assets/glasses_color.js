#pragma strict
	
var glasses : GameObject;	
var mat : Material;
function Start () {
	
	
	
	
}

function Update () {

}

function change_col_white(){

	var whateverColor : Color = new Color(255,255,255);
	var gameObjectRenderer : MeshRenderer = glasses.GetComponent(MeshRenderer);
 
	mat.color = whateverColor;
	gameObjectRenderer.material = mat;
}

function change_col_black(){
 	
 	var whateverColor : Color = new Color(0,0,0);
	var gameObjectRenderer : MeshRenderer = glasses.GetComponent(MeshRenderer);
 
	mat.color = whateverColor;
	gameObjectRenderer.material = mat;
}