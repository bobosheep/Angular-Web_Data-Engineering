  import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-project-description',
  templateUrl: './project-description.component.html',
  styleUrls: ['./project-description.component.css']
})
export class ProjectDescriptionComponent implements OnInit {

  projects: any[] = [{
      title : 'Proj #0 斷句與搜尋 ',
      subtitle : 'Breaking Sentences and Searching', 
      content : '根據提供之新聞資料（約1.9 GB）將所有文章內容做斷句，\
                並將其排序、計算句子重複次數，最後以網頁型式呈現，並提供簡單搜尋功能。',
      links: [{url:'/performance', text:'Performance'},
              {url:'/all_sentence', text:'Sentences'}] 
    },{
      title : 'Proj #1 rsort',
      subtitle : 'A record sorter!', 
      content : '開發一個工具提供文檔排序。開發語言僅限 C/C++ 和 Go。',
      links: []

    },{
      title : 'Proj #2 rgrep',
      subtitle : 'A record search', 
      content : '開發一個工具提供文檔搜尋。',
      links: [{url:'/search', text:'Record Search'}]

    }
  ]

  constructor() { }

  ngOnInit() {
  }

}
