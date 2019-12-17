import { Component, OnInit } from '@angular/core';
import { PageEvent } from '@angular/material/paginator';

import { myHttpService } from './search.service';
import { ifStmt } from '@angular/compiler/src/output/output_ast';

@Component({
  selector: 'search-ui',
  templateUrl: './search-ui.component.html',
  styleUrls: ['./search-ui.component.css']
})
export class SearchUiComponent implements OnInit {

  constructor(private searchService: myHttpService) { }

  ngOnInit() {
  }
  config: any = {
    "url" : 'localhost:5000'
  }
  value: string
  searchResult : any = {}
  sentences: any[] = [] 
  isWaiting: boolean = false
  error: any = false
  pages: string[] = []
  pageEvent: PageEvent
  activePage:number = 1

  pageChange(event: any){
    console.log(event)
    this.pageEvent = event;
    window.scrollTo(0, 0);
    this.searchTerm(this.value, this.pageEvent.pageIndex + 1);
  }

  openUrl(url: string) {
    window.open(url)
  }

  searchTerm(term: string, page: number){
    this.isWaiting = true;
    console.log(term, page);

    this.searchResult = {
      "search_time" : 0,
      "total_results": 0 
     }

    this.searchService.getSearchSentence(term, page)
      .subscribe((result:any) => {
        console.log(result)
        let from = 1;
        let end = parseInt(result.total_results) / 10

        this.activePage = result.page
        this.pages = []
        for(let i = from ; i <= end ; i++)
          this.pages.push(i.toString())

        this.searchResult = {
         "search_time" : result.search_time,
         "total_results": result.total_results 
        }
        this.sentences = result.sentences
        this.isWaiting = false
      }, error => {
        this.error = error
        this.isWaiting = false
      }
      )
    console.log(this.searchResult)
  }
}