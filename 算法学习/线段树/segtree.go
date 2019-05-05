package main

import "fmt"

//线段树


//后序递归构建线段树, 根据arr数组里面原始数据构建线段树 tree (数组形式存放元素).
//node: 表示子树根节点在 tree 数组中的下标
//start, end 为 arr 的下标, 表示要构建线段树子树的原始值区间
func BuildTree(arr, tree []int, node, start, end int){
	if start == end {  //表示叶子节点
		tree[node] = arr[start]
		return
	}
	left_node  := 2 * node + 1  //左节点位置
	right_node := 2 * node + 2 //右节点位置
	mid := (start + end) / 2  //中间值
	BuildTree(arr, tree, left_node, start, mid)  //构建左子树
	BuildTree(arr, tree, right_node, mid + 1, end) //构建右子树
	tree[node] = tree[left_node] + tree[right_node] //计算左右子树的和, 即当前子树根节点的值
}


//将arr[index]的元素的值更新为value, 但其实可以不用更新arr, 只更新树即可
//node表示搜索的起始节点编号
//start和end表示要搜索的子树代表的原始数组的区间
func UpdateTree(tree []int, node, start, end, index, value int){
	if start == end {
		tree[node] = value
		return
	}
	mid := (start + end) / 2
	left_node  := 2 * node + 1
	right_node := 2 * node + 2
	//确定需要改左分支还是右分支
	if index >= start && index <= mid {  //改左分支
		UpdateTree(tree, left_node, start, mid, index, value)
	}else{
		UpdateTree(tree, right_node, mid + 1, end, index, value)
	}
	tree[node] = tree[left_node] + tree[right_node]  //改完之后更新子树根节点
}


//求线段L到R闭区间的和
//node表示要搜索的子树的起始节点在线段树中的编号
//start, end 表示要搜索的子树代表的原始数组的区间
//L, R表示要求值的区间
func QueryTree(tree []int, node, start, end, L, R int) int {
	if R < start || L > end { //子树区间和求值区间不重叠
		return 0
	}
	//if start == end { //叶节点, 直接返回值, 包含在下面的条件里面了
	//	return tree[node]
	//}
	if L<= start && end <= R {  //求值区间包含当前子树, 直接返回子树根节点的值即可
		return tree[node]
	}
	mid := (start + end) / 2
	left_node  := 2 * node + 1
	right_node := 2 * node + 2
	sum_left  := QueryTree(tree, left_node, start, mid, L, R)  //从左子树计算求值子区间的值
	sum_right := QueryTree(tree, right_node, mid + 1, end, L, R) //从右子树计算求值子区间的值
	return sum_left + sum_right
}



func main(){
	const (
		MAX_LEN = 1000
	)
	arr := []int{1,3,5,7,9,11}
	size := 6
	tree := make([]int, MAX_LEN)
	BuildTree(arr, tree, 0, 0, size-1)
	UpdateTree(tree, 0,0, size-1, 4, 6)
	sum := QueryTree(tree, 0, 0, size-1, 3, 5)
	fmt.Printf("tree is: %v\n", tree)
	fmt.Println("sum is:", sum)
}
