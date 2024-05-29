-- 创建商品部表
CREATE TABLE Departments (
  DepartmentID INT PRIMARY KEY,
  ManagerID INT
);

-- 创建职工表
CREATE TABLE Workers (
  WorkerID INT PRIMARY KEY,
  Name VARCHAR(255),
  Address VARCHAR(255),
  DepartmentID INT,
  FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- 创建商品表
CREATE TABLE Products (
  ProductID INT PRIMARY KEY,
  ProductName VARCHAR(255),
  Price DECIMAL(10, 2) CHECK (Price >= 0),
  Model VARCHAR(255),
  InternalCode VARCHAR(255),
  DepartmentID INT,
  FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- 创建生产厂家表
CREATE TABLE Manufacturers (
  ManufacturerID INT PRIMARY KEY,
  ManufacturerName VARCHAR(255),
  ManufacturerAddress VARCHAR(255),
  ManufacturerPrice DECIMAL(10, 2) CHECK (ManufacturerPrice >= 0)
);

-- 插入模拟数据
INSERT INTO Departments (DepartmentID, ManagerID) VALUES
  (1, 1001),
  (2, 1002),
  (3, 1003),
  (4, 1004),
  (5, 1005),
  (6, 1006),
  (7, 1007),
  (8, 1008);

INSERT INTO Workers (WorkerID, Name, Address, DepartmentID) VALUES
  (1001, 'John Doe', '123 Main St', 1),
  (1002, 'Jane Smith', '456 Elm St', 2),
  (1003, 'Michael Johnson', '789 Oak Ave', 1),
  (1004, 'Emily Lee', '567 Pine St', 2),
  (1005, 'David Brown', '321 Maple Rd', 1),
  (1006, 'Lisa Wang', '654 Birch Ln', 2),
  (1007, 'Robert Garcia', '987 Cedar Dr', 1),
  (1008, 'Maria Rodriguez', '234 Willow Ct', 2);

INSERT INTO Products (ProductID, ProductName, Price, Model, InternalCode, DepartmentID) VALUES
  (2001, 'Widget A', 19.99, 'W123 ABC', 'WidgetA123', 1),
  (2002, 'Gadget B', 29.99, 'G456 XYZ', 'GadgetB456', 2),
  (2003, 'Gizmo C', 9.99, 'G789 DEF', 'GizmoC789', 1),
  (2004, 'Widget X', 24.99, 'W987 LMN', 'WidgetX987', 2),
  (2005, 'Gadget Y', 34.99, 'G654 PQR', 'GadgetY654', 1),
  (2006, 'Gizmo Z', 14.99, 'G321 STU', 'GizmoZ321', 2),
  (2007, 'Widget M', 21.99, 'W654 VWX', 'WidgetM654', 1),
  (2008, 'Gadget N', 31.99, 'G987 YZA', 'GadgetN987', 2);

INSERT INTO Manufacturers (ManufacturerID, ManufacturerName, ManufacturerAddress, ManufacturerPrice) VALUES
  (3001, 'Acme Corp', '123 Factory St', 15.00),
  (3002, 'Tech Innovators', '456 Innovation Ave', 25.00),
  (3003, 'Quality Goods Co.', '789 Quality Rd', 10.00),
  (3004, 'Widget World', '987 Widget Blvd', 20.00),
  (3005, 'Gadget Galaxy', '321 Gadget Ln', 30.00),
  (3006, 'Gizmo Industries', '654 Gizmo Rd', 12.00),
  (3007, 'Mega Manufacturers', '234 Mega Dr', 22.00),
  (3008, 'Universal Products', '567 Universal Way', 32.00);
