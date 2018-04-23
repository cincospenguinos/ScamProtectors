import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { Router, NavigationStart } from '@angular/router';
import 'rxjs/add/operator/filter';

import { AuthorizationService } from './../auth/authorization.service';

@Component({
  selector: 'app-body',
  templateUrl: './body.component.html',
  styleUrls: ['./body.component.scss']
})
export class BodyComponent implements OnInit {

  constructor(private router: Router, public auth: AuthorizationService) { }

  ngOnInit() { }

}