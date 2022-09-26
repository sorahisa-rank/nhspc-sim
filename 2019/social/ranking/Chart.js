var Chart=new function(){var self=this;self.draw_chart=function(canvas,y_min,y_max,y_def,h_def,x_int,data,color,marks){var wid=canvas.width;var hei=canvas.height;var pad_l=22;var pad_r=1;var pad_t=6;var pad_b=6;var x_size=0;for(var i in x_int){x_size+=x_int[i][1]-x_int[i][0];}
var get_x=function(x){return pad_l+x*(wid-pad_l-pad_r)/x_size;};var get_y=function(y){return pad_t+(y_max-y)*(hei-pad_t-pad_b)/(y_max-y_min==0?1:y_max-y_min);};canvas.width=wid;var context=canvas.getContext("2d");context.lineWidth=2;context.strokeStyle="#dddddd";context.beginPath();context.moveTo(pad_l,pad_t);context.lineTo(pad_l,hei-pad_b);context.lineTo(wid-pad_r,hei-pad_b);context.lineTo(wid-pad_r,pad_t);context.stroke();context.lineWidth=1;context.moveTo(pad_l,pad_t);context.lineTo(wid-pad_r,pad_t);context.stroke();for(var i in marks){context.beginPath();context.moveTo(get_x(0),get_y(marks[i]));context.lineTo(get_x(x_size),get_y(marks[i]));context.stroke();}
context.fillStyle="#000000";context.textAlign="right";context.textBaseline="middle";if(y_min!=y_max)
context.fillText(y_min.toString(),18,hei-pad_b);context.fillText(y_max.toString(),18,pad_t);for(var i in marks){context.fillText(marks[i].toString(),18,get_y(marks[i]));}
var i=0
var x_cum=0
var x_pos=0
var y_pos=y_def
var h_pos=h_def
var x_b=0
var x_e=0
var tops=[[x_pos,y_pos]]
var bots=[[x_pos,y_pos+h_pos]]
var open_group=function(){context.lineWidth=2;context.strokeStyle="rgb("+color[0]+","+color[1]+","+color[2]+")";context.beginPath();x_b=x_int[i][0];x_e=x_int[i][1];context.moveTo(get_x(x_pos),get_y(y_pos));}
var close_group=function(){x_cum+=x_e-x_b;x_pos=x_cum;context.lineTo(get_x(x_pos),get_y(y_pos));tops.push([x_pos,y_pos]);bots.push([x_pos,y_pos+h_pos])
context.stroke();}
var draw_separator=function(){context.lineWidth=2;context.strokeStyle="#dddddd";context.beginPath();context.moveTo(get_x(x_pos),get_y(y_min));context.lineTo(get_x(x_pos),get_y(y_max));context.stroke();}
open_group();for(var idx in data){var x=data[idx][0];var y=data[idx][1];var h=data[idx][2];while(i<x_int.length&&x_e<=x){close_group();i+=1;if(i<x_int.length){draw_separator();open_group();}else{x_b=0;x_e=0;}}
if(x_b<=x&&x<x_e){x_pos=x_cum+x-x_b;context.lineTo(get_x(x_pos),get_y(y_pos));tops.push([x_pos,y_pos]);bots.push([x_pos,y_pos+h_pos]);y_pos=y;h_pos=h;context.lineTo(get_x(x_pos),get_y(y_pos));tops.push([x_pos,y_pos]);bots.push([x_pos,y_pos+h_pos]);}else{y_pos=y;h_pos=h;context.moveTo(get_x(x_pos),get_y(y_pos));tops.push([x_pos,y_pos]);bots.push([x_pos,y_pos+h_pos]);}}
if(i<x_int.length){close_group();i+=1;}
while(i<x_int.length){draw_separator();open_group();close_group();i+=1;}
context.fillStyle="rgba("+color[0]+","+color[1]+","+color[2]+",0.3)";context.beginPath();context.moveTo(get_x(tops[0][0]),get_y(tops[0][1]));for(var i=0;i<tops.length;i+=1){context.lineTo(get_x(tops[i][0]),get_y(tops[i][1]));}
for(var i=bots.length-1;i>=0;i-=1){context.lineTo(get_x(bots[i][0]),get_y(bots[i][1]));}
context.closePath();context.fill();};};