import { Component, OnInit, Input  } from '@angular/core';

import { User } from '../user';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {

  @Input() user: User;

  constructor() { }

  ngOnInit() {
  }

  signUp(): void {
  }
}
