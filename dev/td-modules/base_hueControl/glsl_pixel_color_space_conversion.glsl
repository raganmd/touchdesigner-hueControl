// Example Pixel Shader
// uniform float exampleUniform;

#include "shaderLib"

out vec4 fragColor;
void main()
{
	vec4 out_color = vec4(1.0);

	vec4 input_color = texture(sTD2DInputs[0], vUV.st);
	vec2 xy_color = color_xy(vec3(input_color.rgb));
	
	out_color.r = xy_color.x;
	out_color.g = xy_color.y;
	out_color.b = input_color.a;
	
	fragColor = TDOutputSwizzle(out_color);
}
