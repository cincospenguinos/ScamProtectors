import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/fromEvent';
import 'rxjs/add/operator/debounceTime';

import { AuthorizationService } from './auth/authorization.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  minHeight: string;
  private _initWinHeight = 0;

  constructor(private auth: AuthorizationService) {
    // Check for authentication and handle if hash present
    auth.handleAuth();
  }

  ngOnInit() {
    Observable.fromEvent(window, 'resize')
      .debounceTime(200)
      .subscribe((event) => this._resizeFn(event));

    this._initWinHeight = window.innerHeight;
    this._resizeFn(null);
  }

  private _resizeFn(e) {
    const winHeight: number = e ? e.target.innerHeight : this._initWinHeight;
    this.minHeight = `${winHeight}px`;
  }
}