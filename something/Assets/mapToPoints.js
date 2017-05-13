#pragma strict

var eye1 : GameObject;
var eye2 : GameObject;
var glasses : GameObject;
var right : GameObject;
var left : GameObject;
var parent : GameObject;
var gex : float;
	var gey : float;
	var ea : float;
	var currentscale : float;
	var truescale : float;
	var gy : float;
	var gx : float;
	var ey : float;
	var ex : float;
	var eyeloc1 : float;
	var distz : float;
	var newloc1 : float;
function Start () {
	parent.transform.localScale = parent.transform.localScale * 1f;
	Application.targetFrameRate = 30;
	
}

function Update () {
	eyeloc1 = right.transform.position.z;
	gy = right.transform.position.y - left.transform.position.y;
	gx = right.transform.position.x - left.transform.position.x;
	ey = eye2.transform.position.y - eye1.transform.position.y;
	ex = eye2.transform.position.x - eye1.transform.position.x;
	currentscale = Mathf.Sqrt(Mathf.Pow(gy,2)+ Mathf.Pow(gx,2));	//make movement based on currentscale
	truescale = Mathf.Sqrt(Mathf.Pow(ey,2)+ Mathf.Pow(ex,2)); // if truescale = 60, "sweet spot"
	if(glasses.transform.localScale.x < 1 && glasses.transform.localScale.x > -1){
		parent.transform.localScale.x = parent.transform.localScale.x * truescale/currentscale;
	}
	if(glasses.transform.localScale.y < 1 && glasses.transform.localScale.y > -1){
	parent.transform.localScale.y = parent.transform.localScale.y * truescale/currentscale;
	}
	if(glasses.transform.localScale.z < 1 && glasses.transform.localScale.z > -1){
	parent.transform.localScale.z = parent.transform.localScale.z * truescale/currentscale;
	}
	newloc1 = right.transform.position.z;
	distz = eyeloc1 - newloc1;
	glasses.transform.position.z = glasses.transform.position.z + distz;
	ea = -Mathf.Atan(ey/ex);
	ea = ea*57.295779; // this # is 180/3.141592653589793238
	var targeta = Quaternion.Euler(0,180,ea);
	glasses.transform.rotation = Quaternion.Slerp(glasses.transform.rotation, targeta, Time.deltaTime*3.0);
	gex = left.transform.position.x - eye1.transform.position.x;
	gey = left.transform.position.y - eye1.transform.position.y;
	glasses.transform.position.x = glasses.transform.position.x - gex;
	glasses.transform.position.y = glasses.transform.position.y - gey;
	glasses.transform.position.x = glasses.transform.position.x -(currentscale-60)*1; //- Mathf.Pow((currentscale-60)*.5,2);// horizontal movement fix
	glasses.transform.position.y = glasses.transform.position.y + ea;
	/*if( ey < 10 ){
		glasses.transform.rotation = eye1.transform.rotation;
	}*/
	
}