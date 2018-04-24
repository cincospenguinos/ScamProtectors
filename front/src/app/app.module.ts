import { BrowserModule, Title } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { FooterComponent } from './footer/footer.component';
import { AuthorizationService } from './auth/authorization.service';
import { CallbackComponent } from './pages/callback/callback.component';
import { BodyComponent } from './body/body.component';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClientModule } from '@angular/common/http';
import { ApiService } from './core/api.service';
import { LoadingComponent } from './core/loading.component';
import { DatePipe } from '@angular/common';
import { UtilsService } from './core/utils.service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './material.module';

import { SocialLoginModule, AuthServiceConfig, GoogleLoginProvider } from "angular5-social-login";

export function provideConfig() {
  let config = new AuthServiceConfig([{
    id: GoogleLoginProvider.PROVIDER_ID,
    provider: new GoogleLoginProvider("127339737905-el6kb2rongp4as3h90madfuifmfdt8s6.apps.googleusercontent.com")
  }]);

return config;
}

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    FooterComponent,
    CallbackComponent,
    BodyComponent,
    LoadingComponent
  ],
  imports: [
    NgbModule.forRoot(),
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MaterialModule,
    SocialLoginModule
  ],
  providers: [ 
    Title,
    AuthorizationService,
    ApiService,
    DatePipe,
    UtilsService,
    {
      provide: AuthServiceConfig,
      useFactory: provideConfig
    }
  ],
  bootstrap: 
  [
    AppComponent
  ]
})

export class AppModule {
}

