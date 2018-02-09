create table builds (
    `sha1` char(40) not null primary key,
    `node` varchar(100) not null, -- e.g. localhost:10001
    `uname` varchar(100) not null, -- e.g. Linux zhen-H270M-D3H 4.13.0-32-generic #35~16.04.1-Ubuntu SMP Thu Jan 25 10:13:43 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
    `toolchain` text not null, -- e.g. gcc-5.4.0,ghc-8.0.2
    `revision` text not null, -- e.g. ghc-1e97e6a11eddf437ab1d948949d6cdcfebc988e0,hadrian-96fb51073fc8afd2dae18c75dd774f2cbbb12317,
    `start_time` timestamp not null,
    `end_time` timestamp not null,
    `log` text not null,
    `exit_code` int not null, -- exit code,
    `status` enum ("initial", "broadcasted") default "initial"
);
