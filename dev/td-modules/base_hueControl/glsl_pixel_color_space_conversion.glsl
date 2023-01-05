// Example Pixel Shader

// uniform float exampleUniform;

uniform vec3 uXVals;
uniform vec3 uYVals;
uniform vec3 uZVals;
uniform float uGamma;

out vec4 fragColor;
void main()
{
	vec4 out_color = vec4(1.0);

	vec4 input_color = texture(sTD2DInputs[0], vUV.st);
	input_color.r = pow(input_color.r, 1.0/uGamma);
	input_color.g = pow(input_color.g, 1.0/uGamma);
	input_color.b = pow(input_color.b, 1.0/uGamma);
	
	vec4 color = vec4(vec3(1.0), 1.0);
	color.r = (input_color.r * uXVals.r) + (input_color.g * uXVals.g) + (input_color.b * uXVals.b);
	color.g = (input_color.r * uYVals.r) + (input_color.g * uYVals.g) + (input_color.b * uYVals.b);
	color.b = (input_color.r * uZVals.r) + (input_color.g * uZVals.g) + (input_color.b * uZVals.b);

	out_color.r = color.r / (color.r + color.g + color.b);
	out_color.g = color.g / (color.r + color.g + color.b);
	
	fragColor = TDOutputSwizzle(out_color);
}
