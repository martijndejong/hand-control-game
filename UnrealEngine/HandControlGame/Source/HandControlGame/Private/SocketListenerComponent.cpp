// SocketListenerComponent.cpp

#include "SocketListenerComponent.h"
#include "Sockets.h"
#include "SocketSubsystem.h"
#include "Networking.h"
#include "Json.h"
#include "JsonUtilities.h"
#include "Async/Async.h"

USocketListenerComponent::USocketListenerComponent()
{
    PrimaryComponentTick.bCanEverTick = false;

    SocketDescription = TEXT("UE5SocketListener");
    Port = 65432;  // Default port; you can change this in the editor if needed
    ListenerSocket = nullptr;
    ConnectionSocket = nullptr;
    ListenThread = nullptr;
    bShouldRun = true;
}

void USocketListenerComponent::BeginPlay()
{
    Super::BeginPlay();
    InitializeSocket();
}

void USocketListenerComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    ShutdownSocket();
    Super::EndPlay(EndPlayReason);
}

void USocketListenerComponent::InitializeSocket()
{
    // Create a TCP socket listener
    ListenerSocket = FTcpSocketBuilder(*SocketDescription)
        .AsReusable()
        .BoundToPort(Port)
        .Listening(8);

    if (ListenerSocket)
    {
        ListenThread = FRunnableThread::Create(this, TEXT("SocketListenerThread"), 0, TPri_Normal);
        UE_LOG(LogTemp, Log, TEXT("Socket listener started on port %d"), Port);
    }
    else
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to create listener socket"));
    }
}

void USocketListenerComponent::ShutdownSocket()
{
    bShouldRun = false;

    if (ListenThread)
    {
        ListenThread->Kill(true);
        delete ListenThread;
        ListenThread = nullptr;
    }

    if (ConnectionSocket)
    {
        ConnectionSocket->Close();
        ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(ConnectionSocket);
        ConnectionSocket = nullptr;
    }

    if (ListenerSocket)
    {
        ListenerSocket->Close();
        ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(ListenerSocket);
        ListenerSocket = nullptr;
    }

    UE_LOG(LogTemp, Log, TEXT("Socket listener stopped"));
}

uint32 USocketListenerComponent::Run()
{
    // Wait for incoming connections
    while (bShouldRun)
    {
        bool Pending;
        if (ListenerSocket->HasPendingConnection(Pending) && Pending)
        {
            ConnectionSocket = ListenerSocket->Accept(TEXT("IncomingConnection"));
            if (ConnectionSocket)
            {
                UE_LOG(LogTemp, Log, TEXT("Accepted connection from client"));
                // Start reading data from the connection
                TArray<uint8> ReceivedData;
                while (bShouldRun && ConnectionSocket->GetConnectionState() == ESocketConnectionState::SCS_Connected)
                {
                    uint32 Size;
                    while (ConnectionSocket->HasPendingData(Size))
                    {
                        ReceivedData.Init(0, FMath::Min(Size, 65507u));

                        int32 Read = 0;
                        ConnectionSocket->Recv(ReceivedData.GetData(), ReceivedData.Num(), Read);

                        // Convert bytes to string
                        FString ReceivedStr = FString(ANSI_TO_TCHAR(reinterpret_cast<const char*>(ReceivedData.GetData())));

                        // Log the received data
                        UE_LOG(LogTemp, Log, TEXT("Received data: %s"), *ReceivedStr);

                        // Handle the received data
                        HandleReceivedData(ReceivedStr);
                    }

                    FPlatformProcess::Sleep(0.01f);
                }

                ConnectionSocket->Close();
                ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(ConnectionSocket);
                ConnectionSocket = nullptr;
            }
        }

        FPlatformProcess::Sleep(0.01f);
    }

    return 0;
}

void USocketListenerComponent::Stop()
{
    bShouldRun = false;
}

void USocketListenerComponent::HandleReceivedData(const FString& Data)
{
    // Split data by newline in case multiple messages are received at once
    TArray<FString> Messages;
    Data.ParseIntoArrayLines(Messages);

    for (const FString& Message : Messages)
    {
        TSharedPtr<FJsonObject> JsonObject;
        TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Message);

        if (FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid())
        {
            FString Action = JsonObject->GetStringField("action");
            FString State = JsonObject->GetStringField("state");

            UE_LOG(LogTemp, Log, TEXT("Parsed action: %s, state: %s"), *Action, *State);

            // Broadcast the OnActionReceived delegate on the game thread
            AsyncTask(ENamedThreads::GameThread, [this, Action, State]()
                {
                    OnActionReceived.Broadcast(Action, State);
                });
        }
        else
        {
            UE_LOG(LogTemp, Warning, TEXT("Failed to parse JSON message: %s"), *Message);
        }
    }
}
