一个代码设计思路-----**依赖倒置原则** (Dependency Inversion Principle)

**依赖倒置原则**的思路是**控制反转(Inversion of Control)**。---- 第三方容器-----> 控制反转容器(IOC Container)

而**控制反转**需要的方法**依赖注入**(Dependency Injection)

Example1 ----- 不合理的设计:

```java
Class car {
  private Framework framework;
  
  car() {
    this.framework = new framework;
  }
  
  public void run() {
    s
  }
}
```



控制反转(Inversion of Control)

