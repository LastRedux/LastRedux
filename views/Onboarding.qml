import QtQuick 2.14

import Kale 1.0

import 'Onboarding'

Item {
  id: root

  property OnboardingViewModel viewModel

  OnboardingWelcome {
    id: welcome

    visible: viewModel && viewModel.currentPageIndex === 0

    onNextPage: viewModel.currentPageIndex = 1

    anchors.fill: parent
  }

  OnboardingConnecting {
    id: connecting

    authUrl: viewModel ? viewModel.authUrl : ''
    hasError: viewModel && viewModel.hasError
    visible: viewModel && viewModel.currentPageIndex === 1

    onBack: viewModel.currentPageIndex = 0
    onTryAgain: viewModel.openNewAuthorizationUrl()
    onTryAuthenticating: viewModel.handleTryAuthenticating()

    anchors.fill: parent
  }

  OnboardingChooseMediaPlayer {
    id: chooseMediaPlayer

    selectedMediaPlayer: viewModel.selectedMediaPlayer
    visible: viewModel && viewModel.currentPageIndex === 2

    onMediaPlayerOptionSelected: (mediaPlayerName) => {
      viewModel.selectedMediaPlayer = mediaPlayerName
    }

    onNextPage: viewModel.currentPageIndex = 3

    anchors.fill: parent
  }

  OnboardingReady {
    id: ready

    visible: viewModel && viewModel.currentPageIndex === 3

    onFinish: viewModel.handleFinish()

    anchors.fill: parent
  }
}