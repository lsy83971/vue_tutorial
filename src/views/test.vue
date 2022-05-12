<template>
  <div class="c-large-table">
    <a-table
      clas
      :loading="loading"
      :columns="columns"
      :row-key="record => record.id"
      :data-source="tableData"
      :row-selection="selected ? { selectedRowKeys: selectedRowKeys, onChange: handleSelect, onSelectAll: handleSelectAll } : null"
      @change="handleTableChange"
      :pagination="pagination"
    >
      <template slot="name" slot-scope="name"> {{ name.first }} {{ name.last }} </template>
    </a-table>
<!-- 虚拟滚动条 -->
    <div class="sc" :style="{height: tableHeight+'px'}">
      <div class="scbc" :style="{height: totalHeight+'px'}"></div>
    </div>
  </div>
</template>

<script>
const ROWS = 15,          // 局部渲染的数据条数
      HEIGHT = 29.6,      // 每行的高度
      TABLEHEIGHT = 446;  // 表格可视高度

export default {
  props: {
    loading: {
      type: Boolean,
      default: false
    },
    dataSource: {
      type: Array,
      default: []
    },
    columns: {
      type: Array,
      default: []
    },
    pagination: {
      type: Object,
      default: {
        current: 1,
        pageSize: 20,
        tota: 0,
        showSizeChanger: true,
        showQuickJumper: true,
        pageSizeOptions: ["20", "50", "100", "200", "500", "1000", "2000"]
      }
    },
    rows: {   // 可视区域展示多少行
      type: Number,
      default: ROWS
    },
    rowHeight: { // 每行的高度
      type: Number,
      default: HEIGHT
    },
    tableHeight: { // 可是区域高度
      type: Number,
      default: TABLEHEIGHT
    },
    selected: { // 是否可选
      type: Boolean,
      default: false
    },
    selectChange: { // 可选的回调
      type: Function,
    },
  },
  data() {
    return {
      scrollEle: '',
      tableData: [],
      selectedRowKeys: [],
      totalHeight: 446,  // 数据总高度
      idx: 0,            // 当前开始下标
    };
  },
  watch: {
    dataSource () {
      const { dataSource, rows, rowHeight } = this
      this.tableData = dataSource.length > rows ? dataSource.slice(0, rows) : dataSource
      this.totalHeight = dataSource.length * rowHeight
    }
  },
  created() {
    const { dataSource, rows, rowHeight } = this
    this.tableData = dataSource.length > rows ? dataSource.slice(0, rows) : dataSource
    this.totalHeight = dataSource.length * rowHeight
  },
  mounted() {
    this.scrollEle = document.querySelector('.c-large-table .sc .scbc');
    document.querySelector('.c-large-table .sc').addEventListener('scroll', this.handleScroll);
  },
  methods: {
    onShowSizeChange(current, pageSize) {
      this.$emit("onShowSizeChange", current, pageSize);
    },
    pageChange(current, pageSize) {
      this.$emit("onChange", current, pageSize);
    },
    handleTableChange() {
      
    },

    handleSelect(d, dl) {
      this.selectedRowKeys = d
      if(this.selected) this.$emit("selectChange", d, dl);
    },
    // 注意全选，需要手动填充数据
    handleSelectAll(d,dl) {
      let keys = [], dates = []
      if(d) {
        keys = this.dataSource.map(item => item.id)
        dates = [...this.dataSource]
      }
      this.handleSelect(keys, dates)
    },
    // 监听虚拟滚轮变化，计算展示的数据
    handleScroll(e) {
      const { scrollTop, scrollHeight } = e.target
      let lenMax = this.dataSource.length, nIdx;

      if(scrollTop === 0) {
        this.tableData = this.dataSource.slice(0, this.rows)
        this.idx = 0
      } else if(scrollTop === (scrollHeight - this.tableHeight)) {
        nIdx = lenMax - this.rows
        this.tableData = this.dataSource.slice(nIdx, nIdx + this.rows)
        this.idx = nIdx
      } else {
        nIdx = Math.ceil(scrollTop * lenMax / scrollHeight)
        if(nIdx !== this.idx && nIdx <= (lenMax - this.rows)) {
          this.tableData = this.dataSource.slice(nIdx, nIdx + this.rows)
          this.idx = nIdx
        }
      }
    },
  },
};
</script>

<style lang="less" >
  .c-large-table {
    position: relative;
    .ant-table-thead > tr > th, .ant-table-tbody > tr > td {
      padding: 4px 10px;
    }
    .sc {
      position: absolute;
      top: 28px;
      right: -6px;
      width: 16px;
      overflow-x: hidden;
      overflow-y: scroll;
      .scbc {
        border-radius: 2px;
        background-color: #F1F1F1;
      }
    }
  }
</style>
