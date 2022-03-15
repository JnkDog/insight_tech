Spring Boot 闭坑

## 1.***\* WARNING \** : Your ApplicationContext is unlikely to start due to a @ComponentScan of the default package.**

出现情况：如果直接将启动文件创建在java文件夹下。 大致情况如下：

----java

---------App.java

----------HelloController.java

其中App.java中有@componentScan的注解，但没有指定范围。

@componentScan(basePackageClasses = 要扫描的类.class所在的位置的包)

分析：Spring Boot的启动类在没有@ComponentScan注解的时候，会默认指定当前启动类所在的包的对象。但由于写在java文件夹下的App类不算任何一个包，所以没有包。

解决：创建一个包把HelloController.java放进去，使用指定范围的@ComponentScan的注解



## 2.Idea里的Maven的镜像设置

方法1.在User Level层面成立，主用户目录下进入.m2目录，创建一个settings.xml文件，输入内容：

```xml
<settings>
    <mirrors>
        <mirror>
            <id>aliyun</id>
            <name>aliyun</name>
            <mirrorOf>central</mirrorOf>
            <!-- 国内推荐阿里云的Maven镜像 -->
            <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
        </mirror>
    </mirrors>
</settings>
```

单个用户成立

方法2.在Gloabl Level层面上成立，进入maven.confg/settings.xml，在<mirrors>your input</mirrors>中输入内容为：

```xml
    <mirror>
        <id>aliyun</id>
        <name>aliyun</name>
        <mirrorOf>central</mirrorOf>
        <!-- 国内推荐阿里云的Maven镜像 -->
        <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
    </mirror>
```


