#define XVALS vec3(0.664511, 0.154324, 0.162028)
#define YVALS vec3(0.283881, 0.668433, 0.047685)
#define ZVALS vec3(0.000088, 0.07231, 0.986039)
#define GAMMA float(0.75)

vec2 color_xy(vec3 inputColor){
	vec2 xy_color;
	
	inputColor.r = pow(inputColor.r, 1.0/GAMMA);
	inputColor.g = pow(inputColor.g, 1.0/GAMMA);
	inputColor.b = pow(inputColor.b, 1.0/GAMMA);

	vec3 color = vec3(1.0);
	color.r = (inputColor.r * XVALS.r) + (inputColor.g * XVALS.g) + (inputColor.b * XVALS.b);
	color.g = (inputColor.r * YVALS.r) + (inputColor.g * YVALS.g) + (inputColor.b * YVALS.b);
	color.b = (inputColor.r * ZVALS.r) + (inputColor.g * ZVALS.g) + (inputColor.b * ZVALS.b);

	xy_color.r = color.r / (color.r + color.g + color.b);
	xy_color.g = color.g / (color.r + color.g + color.b);

	return xy_color;
}