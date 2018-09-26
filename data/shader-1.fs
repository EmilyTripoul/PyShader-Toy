

varying vec3 N;
varying vec3 v;

void main(void)
{
   vec3 L = gl_LightSource[0].position.xyz-v;

   // "Lambert's law"? (see notes)
   // Rather: faces will appear dimmer when struck in an acute angle
   // distance attenuation

   float Idiff = max(dot(normalize(L),N),0.0)*pow(length(L),-2.0); 

   gl_FragColor = vec4(0.0,0,0.5,1.0)+ // purple
                  vec4(1.0,1.0,1.0,1.0)*Idiff; // diffuse reflection
}
