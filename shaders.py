"""
Maria Ines Vasquez Figueroa
18250
Gráficas
ProyectoOpenGL 
Shader
"""

# Los shaders de OpenGL se escriben en un lenguaje de progra llamado GLSL

vertex_shader = """
#version 460
layout (location = 0) in vec4 pos;
layout (location = 1) in vec4 normal;
layout (location = 2) in vec2 texcoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec4 color;
uniform vec4 light;

out vec4 vertexColor;
out vec2 vertexTexcoords;
out vec4 fnormal;
out float fintensity;
out vec4 v3Position;

void main()
{
    float intensity = dot(model * normal, normalize(light - pos));
    fintensity = intensity;
    fnormal=normal;
    v3Position = pos;
    gl_Position = projection * view * model * pos;
    vertexColor = color * intensity;
    vertexTexcoords = texcoords;
}
"""

dance_shader = """
#version 460
layout (location = 0) in vec4 pos;
layout (location = 1) in vec4 normal;
layout (location = 2) in vec2 texcoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec4 color;
uniform vec4 light;
uniform float time;

out vec4 vertexColor;
out vec2 vertexTexcoords;
out vec4 fnormal;

void main()
{
    vec4 newPos= (pos);
    float intensity = dot(model * normal, normalize(light - newPos));
    fnormal=normal;
    gl_Position = (projection * view * model * newPos)-cos(time/30)*80;
    vertexColor = color * intensity;
    vertexTexcoords = texcoords;
}
"""

exp_shader = """
#version 460
layout (location = 0) in vec4 pos;
layout (location = 1) in vec4 normal;
layout (location = 2) in vec2 texcoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec4 color;
uniform vec4 light;
uniform float expl;

out vec4 vertexColor;
out vec2 vertexTexcoords;
out vec4 fnormal;

void main()
{
    vec4 newPos= (pos + (model * normal) * expl/10)/100;
    float intensity = dot(model * normal, normalize(light - pos));
    fnormal=normal;
    gl_Position = projection * view * model * newPos;
    vertexColor = color * intensity;
    vertexTexcoords = texcoords;
}
"""


fragment_shader = """
#version 460
layout (location = 0) out vec4 diffuseColor;

in vec4 vertexColor;
in vec2 vertexTexcoords;

uniform sampler2D tex;

void main()
{
    diffuseColor =  vertexColor * texture(tex, vertexTexcoords);
}
"""

rainbow_shader = """
#version 460
layout (location = 0) out vec4 diffuseColor;

in vec4 fnormal;
in vec4 vertexColor;
in vec2 vertexTexcoords;

uniform sampler2D tex;

void main()
{
  diffuseColor = vec4(fnormal);
}
"""

siren_shader = """
#version 460
layout (location = 0) out vec4 diffuseColor;
precision highp float;
in vec4 fnormal;
uniform float time;

void main()
{
  float theta = time/100;
  
  vec4 dir1 = vec4(cos(theta),0,sin(theta), 0.0); 
  vec4 dir2 = vec4(sin(theta),0,cos(theta), 0.0);
  
  float diffuse1 = pow(dot(fnormal,dir1),2.0);
  float diffuse2 = pow(dot(fnormal,dir2),2.0);
  
  vec4 col1 = diffuse1 * vec4(1,0,0,0.0);
  vec4 col2 = diffuse2 * vec4(0,0,1, 0.0);
  
  diffuseColor = vec4(col1 + col2);
}
"""
ola_shader = """
#version 460
layout (location = 0) out vec4 diffuseColor;

precision highp float;
in vec4 fnormal;
in vec4 vertexColor;
in vec2 vertexTexcoords;
uniform float time;
uniform sampler2D tex;

void main()
{
 diffuseColor = mod(time, 60.0) > 30 ? vec4(1.0, 0.0, 0.0, 9.0) : vec4(1.0, 7.0, 3.0, 0.4);
}

"""

#fallo total
wavy_shader= """
#version 460
layout (location = 0) out vec4 diffuseColor;

in vec4 vertexColor;
in vec2 vertexTexcoords;
uniform sampler2D tex;

void main(){
    vec2 p = vertexTexcoords;
    
    float A = 0.15;
    float w = 10.0 * 3.14159;
    float t = 30.0*3.14159/180.0;
    float y = sin( 10.0 * 3.14159*p.x + 30.0*3.14159/180.0) * 0.15; 
    vec2 uv = vec2(p.x, p.y+y);　 
    vec4 tcolor =  vertexColor * texture(tex, uv); 
    diffuseColor = tcolor; 
}
"""



