import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { Router, NavigationStart } from '@angular/router';
import 'rxjs/add/operator/filter';

import { AuthService } from './../auth/auth.service';

@Component({
  selector: 'app-body',
  templateUrl: './body.component.html',
  styleUrls: ['./body.component.scss']
})
export class BodyComponent implements OnInit {

  constructor(private router: Router, public auth: AuthService) { }

  ngOnInit() { }

  public authenticate(event) {
    alert('Sent token for authentication');
  }
}