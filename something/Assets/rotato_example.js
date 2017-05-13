import UnityEngine.UI;

#pragma strict

var speed : int;
var eye1 : GameObject;
var eye2 : GameObject;
public var inputrotz : InputField; 
public var inputrotx : InputField; 
public var inputroty : InputField; 
public var inputscale : InputField; 
public var inputtranx : InputField;
function Start () {
	

}

function Update () {
	/*if(inputrotz.text != "" && inputrotz.text != "-" && eye1.transform.position.x != parseInt(inputrotz.text)){
		eye2.transform.Translate(-(eye2.transform.position.x - parseInt(inputrotz.text)),0,0);
	}
	if(inputrotx.text != "" && inputrotx.text != "-" && eye2.transform.position.x - parseInt(inputrotx.text)){
		eye1.transform.Translate(-(eye1.transform.position.x - parseInt(inputrotx.text)),0,0);
	}
	if(inputroty.text != "" && inputroty.text != "-" && eye2.transform.position.y - parseInt(inputroty.text)){
		eye1.transform.Translate(0,-(eye1.transform.position.y - parseInt(inputroty.text)),0);
	}
	if(inputscale.text != "" && inputscale.text != "-" && eye1.transform.position.y - parseInt(inputscale.text)){
		eye2.transform.Translate(0,-(eye2.transform.position.y - parseInt(inputscale.text)),0);
	}
	if(inputtranx.text != "" && inputtranx.text != "-"){
		var derp : float = speed * Time.deltaTime * parseInt(inputtranx.text);
		
	}*/
}