

varying vec3 v;
varying vec3 N;


void main(void)
{

   v = gl_ModelViewMatrix * gl_Vertex;
   N = gl_NormalMatrix * gl_Normal;

   gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;

}
