create table `t_cities`
(
	`id` int primary key auto_increment,
    `name` varchar(50) not null,
    `onsail` int default 0,
    `deal` int default 0,
    unique index city_name(`name`)
);

create table `t_regions`
(
	`id` int primary key auto_increment,
    `name` varchar(50) not null,
    `cityId` int not null,
    `onsail` int default 0,
    `deal` int default 0,
    unique index region_name(`name`),
    index(`cityId`)
);

create table `t_info`
(
	`id` int primary key auto_increment,
    `name` varchar(255) not null,
    `deal` boolean not null,
    `cityId` int not null,
    `regionId` int default 0,
    `type` varchar(20) not null,
    `area` float not null,
    `totalPrice` float not null,
    `unitPrice` float not null,
    `dealTime` date default null,
    index(`cityId`), index(`regionId`),
    index(`type`), index(`area`)
);