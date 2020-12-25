import QtQuick 2.14

import Kale 1.0

import 'Onboarding'

Item {
  id: root

  property OnboardingViewModel viewModel

  OnboardingWelcome {
    id: welcome

    visible: viewModel && viewModel.currentPage === 0

    onNextPage: viewModel.currentPage = 1

    anchors.fill: parent
  }

  OnboardingConnecting {
    id: connecting

    authUrl: viewModel ? viewModel.authUrl : ''
    hasError: viewModel && viewModel.hasError
    visible: viewModel && viewModel.currentPage === 1

    onBack: viewModel.currentPage = 0
    onTryAgain: viewModel.openNewAuthorizationUrl()
    onTryAuthenticating: viewModel.authenticate()

    anchors.fill: parent
  }

  OnboardingReady {
    id: ready

    visible: viewModel && viewModel.currentPage === 2

    onFinish: viewModel.finish()

    anchors.fill: parent
  }
}