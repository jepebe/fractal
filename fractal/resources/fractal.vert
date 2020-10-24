#version 400 core
layout (location=0) in vec3 position;
layout (location=1) in vec2 tex;

uniform mat4 projection_view;
uniform mat4 model;

out vec2 tex_coord;

void main() {
    gl_Position = projection_view * model * vec4(position, 1.0f);
    tex_coord = tex;
}