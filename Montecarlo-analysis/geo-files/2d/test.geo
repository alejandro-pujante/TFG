lc = 2;
//+
Point(1) = {-100, -100, 0, lc};
//+
Point(2) = {-100, 100, 0, lc};
//+
Point(3) = {100, 100, 0, lc};
//+
Point(4) = {100, -100, 0, lc};
//+
Line(1) = {1, 2};
Line(2) = {1, 4};
Line(3) = {2, 3};
Line(4) = {3, 4};
//+
Curve Loop(1) = {3, 4, -2, 1};
//+
Plane Surface(1) = {1};
//+
Physical Surface("all", 5) = {1};
