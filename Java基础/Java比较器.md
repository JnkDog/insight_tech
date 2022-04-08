# Java 排序之比较器
## Comparable
Comparable 是排序接口，若一个类实现了 Comparable 接口，就意味着 “该类支持排序”。假设现在存在 “实现 Comparable 接口的类的对象的集合（或数组）”，则该集合（或数组）可以通过 Collections.sort（或 Arrays.sort）进行排序。

实现 Comparable 接口的类必须实现 compareTo 方法，对象就可以比较大小。假设我们通过 x.compareTo(y) 来 “比较 x 和 y 的大小”。若返回 “负数”，意味着 “x 比 y 小”；返回 “零”，意味着 “x 等于 y”；返回 “正数”，意味着 “x 大于 y”。

Comparable 定义在想要实现排序对象的类的内部，并且重写compareTo方法

## Comparator
也是一个接口，可以用来当想要排序的类没有实现Comparable接口
Comparator 定义在想要实现排序对象的类的** 外部 **，并且重写compare方法。
当一个类未定义比较规则，并且我们想要对其进行排序时，会使用你匿名内部类的方式或者重新自定义一个类并实现Comparator接口的方式来达到这个目的。耦合度较低

```Java
package java.util;
public interface Comparator<T> {
    int compare(T o1, T o2);
    boolean equals(Object obj);
}
```
只需要实现compare方法就行，equals是Object的对像方法，已经重写了的
int compare(T o1, T o2) 是 “比较 o1 和 o2 的大小”。返回 “负数”，意味着 “o1 比 o2 小”；返回 “零”，意味着 “o1 等于 o2”；返回 “正数”，意味着 “o1 大于 o2”

这里o1表示位于前面的对象，o2表示后面的对象

返回-1（或负数），表示不需要交换01和02的位置，o1排在o2前面，asc (o1 < o2)
返回1（或正数），表示需要交换01和02的位置，o1排在o2后面，desc   (o1 > o2)
简单记忆为1代表true需要**转换位置**，写的时候拿笔写下

## 比较的原理
实际上比较器的操作，就是经常听到的二叉树的排序算法。

排序的基本原理：使用第一个元素作为根节点，之后如果后面的内容比根节点小，则放在左子树，如果内容比根节点的内容要大，则放在右子树。